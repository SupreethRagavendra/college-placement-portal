<?php

namespace Tests\Unit;

use Tests\TestCase;
use App\Http\Controllers\AdminReportController;

class AdminReportControllerTest extends TestCase
{
    /**
     * Test time formatting for export
     *
     * @return void
     */
    public function testFormatTimeForExport()
    {
        // We'll need to use reflection to test the private method
        $controller = new AdminReportController();
        $reflection = new \ReflectionClass($controller);
        $method = $reflection->getMethod('formatTimeForExport');
        $method->setAccessible(true);

        // Test seconds only
        $result = $method->invoke($controller, 30);
        $this->assertEquals('30 seconds', $result);

        // Test minutes only
        $result = $method->invoke($controller, 120);
        $this->assertEquals('2 minutes', $result);

        // Test minutes and seconds
        $result = $method->invoke($controller, 150);
        $this->assertEquals('2m 30s', $result);

        // Test hours only
        $result = $method->invoke($controller, 7200);
        $this->assertEquals('2h', $result);

        // Test hours and minutes
        $result = $method->invoke($controller, 7500);
        $this->assertEquals('2h 5m', $result);

        // Test hours, minutes and seconds
        $result = $method->invoke($controller, 7530);
        $this->assertEquals('2h 5m 30s', $result);
    }
}