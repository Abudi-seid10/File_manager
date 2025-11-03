# Security Policy

## Supported Versions

Currently supported versions of File Organizer:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Create a Public Issue

Please do not create a public GitHub issue for security vulnerabilities.

### 2. Report Privately

Send details of the vulnerability to the project maintainers via:
- GitHub Security Advisories (preferred)
- Direct message to repository owner

### 3. Include Details

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information

### 4. Response Time

- We will acknowledge receipt within 48 hours
- We will provide a detailed response within 7 days
- We will work on a fix and keep you updated on progress

### 5. Disclosure

- We will work with you to understand and resolve the issue
- Once fixed, we will publicly disclose the vulnerability
- You will be credited for the discovery (unless you prefer to remain anonymous)

## Security Best Practices

When using File Organizer:

1. **File Permissions**: Ensure the application has appropriate file system permissions
2. **Directory Selection**: Only select directories you trust
3. **Dry Run Mode**: Use dry run mode to preview changes before applying
4. **Backups**: Always maintain backups of important files
5. **Configuration**: Review config.json for sensitive paths before sharing

## Known Security Considerations

1. **File Hashing**: Uses SHA256 for duplicate detection (cryptographically secure)
2. **File Operations**: All file operations include error handling and validation
3. **Input Validation**: Directory paths are validated before processing
4. **Logging**: Logs may contain file paths - review before sharing

## Security Updates

Security updates will be released as soon as possible after verification. Users will be notified through:
- GitHub releases
- Security advisories
- README updates

Thank you for helping keep File Organizer secure!
