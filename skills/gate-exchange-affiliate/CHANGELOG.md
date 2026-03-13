# Changelog

## [2026.3.12-2] - 2026-03-12

### Changed
- Restructured SKILL.md to follow standard template format
- Added formal Workflow section with 6 defined steps
- Added Judgment Logic Summary table with 14 conditions
- Added standardized Report Template
- Updated README.md with Architecture section
- Reformatted scenarios.md to standard Scenario format

### Improved
- Better alignment with skill-validator requirements
- Clearer separation of workflow steps and data extraction
- More structured documentation organization

## [2026.3.12-1] - 2026-03-12

### Added
- Initial release of Gate Exchange Affiliate skill
- Support for partner transaction history queries
- Support for partner commission history queries
- Support for partner subordinate list queries
- Automatic handling of >30 day queries (up to 180 days)
- Comprehensive error handling and user guidance
- Affiliate program application instructions

### Features
- Query commission amount, trading volume, net fees, customer count, and trading users
- Time-range specific queries with automatic request splitting
- User-specific contribution analysis
- Team performance report generation
- Multi-language trigger phrase support (internally handled in English)

### Technical
- Uses Partner APIs only (Agency APIs deprecated)
- Implements pagination for large result sets
- Handles Unix timestamp conversion
- Provides detailed API parameter documentation