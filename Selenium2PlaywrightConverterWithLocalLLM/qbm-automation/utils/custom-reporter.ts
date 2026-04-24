import { Reporter, TestCase, TestResult, FullConfig, FullSuite } from '@playwright/test/reporter';

class CustomReporter implements Reporter {
    onBegin(config: FullConfig, suite: FullSuite) {
        console.log(`\n=================================================`);
        console.log(`🚀 QBM Automation Suite started: ${suite.allTests().length} tests`);
        console.log(`=================================================\n`);
    }

    onTestBegin(test: TestCase) {
        console.log(`👉 Starting test: ${test.title}`);
    }

    onTestEnd(test: TestCase, result: TestResult) {
        const status = result.status === 'passed' ? '✅ PASSED' : '❌ FAILED';
        console.log(`${status}: ${test.title} [${result.duration}ms]`);
        if (result.error) {
            console.log(`   Detailed Error: ${result.error.message}`);
        }
    }

    onEnd(result: any) {
        console.log(`\n=================================================`);
        console.log(`🏁 Test Execution Finished: ${result.status.toUpperCase()}`);
        console.log(`=================================================\n`);
    }
}

export default CustomReporter;
