## Description
Brief description of changes.

## Type of Change
- [ ] New skill
- [ ] Skill enhancement (existing skill content update)
- [ ] Bug fix (tooling or workflow)
- [ ] New tool/CLI command
- [ ] Documentation update
- [ ] CI/CD pipeline change
- [ ] Other: ___

## Skill Quality Checklist (for new/modified skills)
- [ ] YAML frontmatter includes 
ame and description
- [ ] Input Contract table is present and complete
- [ ] Output Contract table is present and complete
- [ ] Prerequisites checklist is present
- [ ] Step-by-step workflow section is present
- [ ] AI Agent Integration section with Autonomy Level, Agent, and Human Gates
- [ ] Success Criteria checklist is present
- [ ] Runnable examples (YAML, scripts, configs) are included

## Testing
- [ ] python tools/validate_skills.py --project-root . passes
- [ ] python tools/generate_docs.py --project-root . runs successfully
- [ ] New skill scaffolds correctly with python tools/scaffold_skill.py
- [ ] Python tests pass: pytest tests/ -v

## Cross-References
- List any skills that reference or are referenced by this change
- e.g., "s14 references s15 output — verified cross-reference is correct"
