---
name: cloakbrowser-testing
description: >
  Execute comprehensive test suites using CloakBrowser for end-to-end web application
  testing, accessibility testing, visual regression testing, and chaos testing validation.
  Use this skill whenever the user says "test my app", "run test suite", "browser test",
  "verify functionality", "test in CloakBrowser", "run E2E tests", or needs to validate
  application behavior before and after chaos experiments. Also trigger after CI/CD
  pipeline setup (s04) and before chaos experiment execution (s12+) to establish baseline
  behavior. CloakBrowser (https://github.com/CloakHQ/CloakBrowser) is used for its
  enhanced privacy, anti-detection capabilities, and agent-friendly automation API.
---

# CloakBrowser Testing (s11)

## Purpose
Execute deep, comprehensive test case execution using CloakBrowser as the primary browser automation engine. Establish pre-chaos behavioral baselines, validate post-deployment functionality, and generate test evidence that feeds into resilience scoring and postmortem learning.

---

## Prerequisites
- [ ] PRD and user flows from s01 (BA Requirements) or s01-1 (User Flow Writing)
- [ ] Pipeline YAML from s04 (Pipeline Design)
- [ ] Service deployed and accessible in target environment
- [ ] CloakBrowser installed and configured
- [ ] Test environment URLs available

## Input Contract

| Input | Source | Required |
|---|---|---|
| PRD with acceptance criteria | s01 (workflow_context) | Yes |
| Deployed application URL(s) | s04, s05 (pipeline outputs) | Yes |
| Feature flag states (what's enabled) | s08 output | No |
| Expected steady state behavior | s15 output | No |
| Test framework preference | s02 taste (testing category) | No |
| Previous test results (for regression) | s25 (postmortem feedback) | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Test execution report | `.commandcode/artifacts/test-report.html` | HTML |
| Test results (JUnit XML) | `.commandcode/artifacts/test-results.xml` | XML |
| Coverage report | `.commandcode/artifacts/coverage/index.html` | HTML |
| Screenshot evidence | `.commandcode/artifacts/screenshots/` | PNG |
| Accessibility audit report | `.commandcode/artifacts/a11y-report.html` | HTML |
| Performance metrics | `.commandcode/artifacts/perf-metrics.json` | JSON |
| Pre-chaos baseline data | s18 (game day), s24 (scoring) | JSON |
| Test context | workflow_context.artifacts | YAML object |

---

## Testing Strategy

```
PRE-DEPLOYMENT          POST-DEPLOYMENT         PRE-CHAOS              POST-CHAOS
     │                       │                      │                      │
Smoke tests           Regression suite      Baseline capture       Regression rerun
Unit tests            E2E flows             Performance profile    Compare baseline
Lint + SAST           A11y audit            Screenshot baseline    Visual diff
                       Load test (k6)                              Resilience evidence
```

---

## CloakBrowser Setup

### Installation
```bash
# CloakBrowser is a Chromium-based browser with enhanced privacy features
# Download from: https://github.com/CloakHQ/CloakBrowser

# For automated testing, use the headless API:
npm install cloakbrowser-playwright   # Playwright-compatible API
# or
pip install cloakbrowser-client        # Python client
```

### Configuration
```yaml
# .cloakbrowserrc.yaml
browser:
  executable: "/Applications/CloakBrowser.app/Contents/MacOS/CloakBrowser"
  headless: true
  privacy:
    fingerprint_randomization: true
    canvas_noise: true
    webgl_noise: true
    user_agent_rotation: true
  viewport:
    width: 1920
    height: 1080

test:
  base_url: "https://<SERVICE>.staging.company.com"
  screenshot_on_failure: true
  video_on_failure: true
  timeout: 30000
  retries: 2

reporting:
  output_dir: ".commandcode/artifacts/"
  formats: ["html", "json", "junit"]
  screenshot_comparison_threshold: 0.01  # 1% pixel difference allowed
```

---

## Test Categories

### 1. Smoke Tests (Run First)
```typescript
// smoke.spec.ts — Ensures basic functionality works
import { test, expect } from '@playwright/test'; // Using CloakBrowser as engine

test.describe('Smoke Tests', () => {
  test('health endpoint returns 200', async ({ request }) => {
    const response = await request.get('/health');
    expect(response.status()).toBe(200);
    const body = await response.json();
    expect(body.status).toBe('healthy');
  });

  test('homepage loads without errors', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', error => errors.push(error.message));

    await page.goto('/');
    await expect(page.locator('h1')).toBeVisible();
    expect(errors).toHaveLength(0);
  });

  test('critical API endpoints respond', async ({ request }) => {
    const endpoints = ['/api/v1/status', '/api/v1/config'];
    for (const endpoint of endpoints) {
      const response = await request.get(endpoint);
      expect(response.status()).toBe(200);
    }
  });
});
```

### 2. E2E Flow Tests
```typescript
// e2e-checkout.spec.ts — Complete user journey
test.describe('Checkout Flow E2E', () => {
  test('complete purchase journey', async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('[data-testid="email"]', process.env.TEST_EMAIL!);
    await page.fill('[data-testid="password"]', process.env.TEST_PASSWORD!);
    await page.click('[data-testid="login-button"]');

    // Browse product
    await page.goto('/products');
    await page.click('[data-testid="product-card"]:first-child');

    // Add to cart
    await page.click('[data-testid="add-to-cart"]');
    await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');

    // Checkout
    await page.goto('/checkout');
    await page.fill('[data-testid="card-number"]', '4242424242424242');
    await page.click('[data-testid="place-order"]');

    // Verify success
    await expect(page.locator('[data-testid="order-confirmed"]')).toBeVisible();
    await expect(page.locator('[data-testid="order-number"]')).not.toBeEmpty();
  });
});
```

### 3. Accessibility Audit
```typescript
// a11y.spec.ts — WCAG compliance check
import { injectAxe, checkA11y } from 'axe-playwright';

test.describe('Accessibility Audit', () => {
  const criticalPages = ['/', '/login', '/checkout', '/account', '/products'];

  for (const path of criticalPages) {
    test(`a11y audit: ${path}`, async ({ page }) => {
      await page.goto(path);
      await injectAxe(page);
      const results = await checkA11y(page, null, {
        detailedReport: true,
        detailedReportOptions: { html: true },
      });
      expect(results.violations.filter(v => v.impact === 'critical')).toHaveLength(0);
    });
  }
});
```

### 4. Pre-Chaos Baseline Capture
```typescript
// baseline-capture.spec.ts — Captures performance + behavior before chaos
test.describe('Pre-Chaos Baseline', () => {
  const metrics: BaselineMetrics = {
    timestamp: new Date().toISOString(),
    pages: {},
  };

  test('capture performance metrics for all critical pages', async ({ page }) => {
    const criticalPages = ['/', '/checkout', '/api/v1/payments'];

    for (const path of criticalPages) {
      await page.goto(path, { waitUntil: 'networkidle' });

      const perfEntries = await page.evaluate(() => {
        const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        return {
          domContentLoaded: navigation.domContentLoadedEventEnd - navigation.startTime,
          loadComplete: navigation.loadEventEnd - navigation.startTime,
          firstPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime,
        };
      });

      metrics.pages[path] = perfEntries;
    }

    // Write baseline for post-chaos comparison
    await page.evaluate(
      (m) => window.localStorage.setItem('pre-chaos-baseline', JSON.stringify(m)),
      metrics,
    );
  });

  test('capture visual baseline screenshots', async ({ page }) => {
    await page.goto('/checkout');
    await page.screenshot({
      path: '.commandcode/artifacts/screenshots/baseline-checkout.png',
      fullPage: true,
    });
  });
});
```

### 5. Post-Chaos Regression
```typescript
// post-chaos-regression.spec.ts — Compares against baseline
test.describe('Post-Chaos Regression', () => {
  test('performance within 20% of baseline', async ({ page }) => {
    const baseline = JSON.parse(
      await page.evaluate(() => localStorage.getItem('pre-chaos-baseline') || '{}'),
    );

    for (const [path, baselineMetrics] of Object.entries(baseline.pages || {})) {
      await page.goto(path as string, { waitUntil: 'networkidle' });

      const current = await page.evaluate(() => {
        const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
        return nav.loadEventEnd - nav.startTime;
      });

      const maxAllowed = (baselineMetrics as any).loadComplete * 1.2; // 20% tolerance
      expect(current).toBeLessThanOrEqual(maxAllowed);
    }
  });

  test('visual diff within threshold', async ({ page }) => {
    await page.goto('/checkout');
    expect(await page.screenshot({ fullPage: true })).toMatchSnapshot({
      maxDiffPixelRatio: 0.01,
      threshold: 0.1,
    });
  });
});
```

---

## Test Execution Commands

```bash
# Run full test suite
npx playwright test --config=playwright.config.ts

# Run only smoke tests (fast feedback)
npx playwright test --grep "@smoke"

# Run E2E tests tagged for pre-chaos
npx playwright test --grep "@pre-chaos"

# Run with CloakBrowser explicitly
CLOAKBROWSER_PATH=/Applications/CloakBrowser.app npx playwright test

# Generate HTML report
npx playwright show-report .commandcode/artifacts/test-report.html

# Run accessibility audit only
npx playwright test --grep "a11y"
```

---

## Test Evidence for Chaos Validation

After running tests (both pre and post chaos), produce this evidence package:

```yaml
# test-evidence.yaml — consumed by s24 resilience scoring
evidence:
  test_suite: "full-regression"
  duration_seconds: 245
  total_tests: 87
  passed: 84
  failed: 2
  skipped: 1
  pass_rate: 96.55

  pre_chaos_baseline:
    checkout_page_load_ms: 1250
    payment_api_latency_ms: 180
    error_rate_percent: 0.02

  post_chaos_comparison:
    checkout_page_load_ms: 1380        # +10.4% (within 20% threshold)
    payment_api_latency_ms: 210        # +16.7% (within 20% threshold)
    error_rate_percent: 0.05           # +0.03pp (within 5% threshold)
    visual_diff_score: 0.005           # 0.5% (within 1% threshold)

  accessibility:
    critical_violations: 0
    serious_violations: 1
    moderate_violations: 3

  verdict: "PASS_ALL_THRESHOLDS"

  screenshots:
    - baseline-checkout.png
    - post-chaos-checkout.png
    - diff-checkout.png
```

---

## Integration with Workflow

### Before Chaos (s12 → s18)
```
s11 produces: pre-chaos baseline + full test evidence
   ↓ feeds into:
s18 (game day) — confirms system healthy before fault injection
s24 (scoring) — baseline for comparison
```

### After Chaos (s18 → s21)
```
s11 runs again: same test suite against post-chaos state
   ↓ comparison feeds into:
s21 (alerting) — regression alerts if thresholds exceeded
s24 (scoring) — resilience score calculation
s25 (postmortem) — evidence for RCA
```

---

## Test Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  expect: { timeout: 10000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : 2,

  use: {
    baseURL: process.env.BASE_URL || 'https://staging.company.com',
    channel: 'chromium',
    launchOptions: {
      executablePath: process.env.CLOAKBROWSER_PATH,
    },
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
  ],

  reporter: [
    ['html', { outputFolder: '.commandcode/artifacts/test-report' }],
    ['junit', { outputFile: '.commandcode/artifacts/test-results.xml' }],
    ['json', { outputFile: '.commandcode/artifacts/test-results.json' }],
  ],
});
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L2 | AI creates tests 10x faster with self-healing |
| Target | L3 | AI generates and maintains test suite, human approves baselines |

### Harness AI Agent

**Agent**: Harness AI Test Agent
**Capabilities**:
- Natural language test creation (10x faster)
- Self-healing tests (70% maintenance reduction)
- Intent-based testing adapting to UI changes

### Human Gates

- Test baseline approval
- Test coverage acceptance
- Visual regression threshold

### Fallback

Manual test creation following Playwright and CloakBrowser documentation

---

## Success Criteria
- [ ] Smoke tests pass (100% pass rate for /health, homepage, critical APIs)
- [ ] E2E flow tests pass (all critical user journeys)
- [ ] Zero critical accessibility violations
- [ ] Pre-chaos baseline captured and stored
- [ ] Test results in JUnit XML format for pipeline CV integration
- [ ] Screenshot evidence saved for visual regression comparison
- [ ] Test evidence YAML produced for s24 scoring
- [ ] Test execution time < 10 minutes (fast feedback loop)
- [ ] Coverage report shows > 80% for critical paths
