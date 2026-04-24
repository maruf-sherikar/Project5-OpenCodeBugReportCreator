import { Reporter, TestCase, TestResult } from '@playwright/test/reporter';

class CustomReporter implements Reporter {
    onBegin(config, suite) {
        console.log(`\n🚀 Starting test execution with ${suite.allTests().length} tests\n`);
    }

    onTestBegin(test: TestCase) {
        console.log(`🧪 Running: ${test.title}`);
    }

    onTestEnd(test: TestCase, result: TestResult) {
        const status = result.status === 'passed' ? '✅' : '❌';
        console.log(`${status} Finished: ${test.title} (${result.duration}ms)`);
        if (result.error) {
            console.log(`   └─ Error: ${result.error.message}`);
        }
    }

    onEnd(result) {
        console.log(`\n🏁 Test Run Result: ${result.status.toUpperCase()}`);
    }
}

export default CustomReporter;
