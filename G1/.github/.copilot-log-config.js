// OOM Development Workflow Configuration
// Complements copilot-instructions.md with automation and testing protocols
// Handles development cycle, error resolution, and validation processes
// For architectural guidance and code patterns, see copilot-instructions.md

module.exports = {
  // Log file paths following project structure
  logFile: 'logs/oom-web-output.log',
  activityLog: 'logs/OOM_ACTIVITY_LOG.md',
  runtimeLogFile: 'logs/oom-runtime-errors.log',
  errorLogFile: 'logs/oom-compilation-errors.log',
  testResultsLog: 'logs/oom-test-results.log',
  
  // Development cycle automation
  afterEachChange: [
    // 1. Write change summary to OOM_ACTIVITY_LOG.md (follows project documentation structure)
    // 2. Test functionality and capture output to oom-web-output.log
    // 3. Capture runtime errors to oom-runtime-errors.log
    // 4. Run scripts/oom-log-reader.py to check compilation and runtime errors
    // 5. Execute test_e2e_comprehensive.py for full system validation
    // 6. Auto-fix errors before proceeding (100% success criteria requirement)
  ],
  
  // System prompts following OOM documentation standards
  systemPrompt: [
    'Development Cycle: After code changes, test affected components. Log output to logs/oom-web-output.log and errors to logs/oom-runtime-errors.log.',
    'Testing Protocol: Execute test_e2e_comprehensive.py for complete validation. Run test_backend_comprehensive.py and frontend tests for component testing.',
    'Browser Testing: Use Safari WebDriver as default browser for all UI testing. Chrome is not permitted for testing operations.',
    'Documentation: Update logs/OOM_ACTIVITY_LOG.md following project documentation structure. Include change summaries and test results.',
    'Error Resolution: Use scripts/oom-log-reader.py for error analysis. Auto-fix compilation and runtime errors. Maintain 100% test success criteria.',
    'Virtual Environment: Use .venv virtual environment for all Python operations. Activate before running scripts and tests.',
    'Task Automation: Proceed automatically after successful tests. Only request user confirmation for critical errors or breaking changes.',
    'Final Validation: Run comprehensive test suite before commits. Execute test_e2e_comprehensive.py, test_workflow_complete.py, and test_backend_comprehensive.py.',
    'Git Integration: Follow project naming conventions for commits. Use descriptive messages aligned with OOM project standards.',
    'Production Readiness: Ensure all tests pass, no compilation errors, and runtime errors resolved before task completion.',
    'Script Execution: Use current shell environment, dont switch shell, bind to one terminal. Run Python scripts with .venv environment. Auto-execute without permission requests.',
    'Keep a copy of all the input instructions given by user into logs/OOM_INSTRUCTION_HISTORY_LOG.md for future reference.',
  ],
  
  // Project-specific configuration
  projectConfig: {
    name: 'oom',
    virtualEnv: '.venv',
    testSuite: 'test_e2e_comprehensive.py',
    backendTests: 'test_backend_comprehensive.py',
    frontendTests: 'tests/frontend/',
    logReader: 'scripts/oom-log-reader.py',
    successCriteria: 100, // 100% test success rate requirement
    documentationStyle: 'README.md', // Follow existing docs structure
    defaultBrowser: 'safari', // Use Safari as default browser for testing
    browserDriver: 'Safari', // Safari WebDriver configuration
  },
  
  // File naming conventions (following project standards)
  fileNaming: {
    pythonFiles: 'snake_case', // e.g., data_processor.py
    jsFiles: 'kebab-case', // e.g., data-upload.tsx
    directories: 'kebab-case', // e.g., data-processing/
    constants: 'UPPER_SNAKE_CASE', // e.g., API_BASE_URL
    components: 'PascalCase', // e.g., DataUpload
    functions: 'camelCase', // e.g., processData
  }
};
