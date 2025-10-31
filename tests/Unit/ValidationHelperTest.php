<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ValidationHelperTest extends TestCase
{
    /**
     * Test email validation logic
     */
    public function test_valid_email_format()
    {
        $validEmails = [
            'test@example.com',
            'user.name@example.co.uk',
            'user+tag@example.com',
            'user123@domain.org',
            'test.email@subdomain.example.com'
        ];

        foreach ($validEmails as $email) {
            $this->assertTrue(
                filter_var($email, FILTER_VALIDATE_EMAIL) !== false,
                "Email '{$email}' should be valid"
            );
        }
    }

    public function test_invalid_email_format()
    {
        $invalidEmails = [
            'invalid.email',
            '@example.com',
            'user@',
            'user space@example.com',
            'user@domain',
            'user@@example.com',
            'user@.com',
            'user@domain..com'
        ];

        foreach ($invalidEmails as $email) {
            $this->assertFalse(
                filter_var($email, FILTER_VALIDATE_EMAIL) !== false,
                "Email '{$email}' should be invalid"
            );
        }
    }

    /**
     * Test password strength validation
     */
    public function test_password_strength_validation()
    {
        // Strong passwords
        $strongPasswords = [
            'Password123!',
            'MySecure@Pass2024',
            'Complex#Pass1',
            'StrongP@ssw0rd'
        ];

        foreach ($strongPasswords as $password) {
            $this->assertTrue(
                $this->isStrongPassword($password),
                "Password '{$password}' should be strong"
            );
        }

        // Weak passwords
        $weakPasswords = [
            'password',
            '12345678',
            'Password',
            'password123',
            'P@ss',
            'PASSWORD123!'
        ];

        foreach ($weakPasswords as $password) {
            $this->assertFalse(
                $this->isStrongPassword($password),
                "Password '{$password}' should be weak"
            );
        }
    }

    /**
     * Test percentage calculation
     */
    public function test_percentage_calculation()
    {
        $this->assertEquals(50.0, $this->calculatePercentage(5, 10));
        $this->assertEquals(100.0, $this->calculatePercentage(10, 10));
        $this->assertEquals(0.0, $this->calculatePercentage(0, 10));
        $this->assertEquals(75.0, $this->calculatePercentage(75, 100));
        $this->assertEquals(33.33333333333333, $this->calculatePercentage(1, 3), '', 0.01);
    }

    public function test_percentage_with_zero_total_returns_zero()
    {
        $this->assertEquals(0.0, $this->calculatePercentage(5, 0));
    }

    public function test_percentage_with_negative_values()
    {
        $this->assertEquals(-50.0, $this->calculatePercentage(-5, 10));
        $this->assertEquals(-50.0, $this->calculatePercentage(5, -10));
    }

    /**
     * Test time formatting
     */
    public function test_format_time_seconds_only()
    {
        $this->assertEquals('30 seconds', $this->formatTime(30));
        $this->assertEquals('1 second', $this->formatTime(1));
        $this->assertEquals('59 seconds', $this->formatTime(59));
        $this->assertEquals('0 seconds', $this->formatTime(0));
    }

    public function test_format_time_minutes()
    {
        $this->assertEquals('1 minute', $this->formatTime(60));
        $this->assertEquals('2 minutes', $this->formatTime(120));
        $this->assertEquals('2m 30s', $this->formatTime(150));
        $this->assertEquals('5m 45s', $this->formatTime(345));
    }

    public function test_format_time_hours()
    {
        $this->assertEquals('1h', $this->formatTime(3600));
        $this->assertEquals('2h 5m', $this->formatTime(7500));
        $this->assertEquals('2h 5m 30s', $this->formatTime(7530));
        $this->assertEquals('1h 30m', $this->formatTime(5400));
    }

    public function test_format_time_large_values()
    {
        $this->assertEquals('25h 30m', $this->formatTime(91800)); // 25.5 hours
        $this->assertEquals('1h', $this->formatTime(3600));
    }

    /**
     * Test grade calculation
     */
    public function test_grade_calculation()
    {
        $this->assertEquals('A', $this->calculateGrade(95));
        $this->assertEquals('A', $this->calculateGrade(90));
        $this->assertEquals('B', $this->calculateGrade(85));
        $this->assertEquals('B', $this->calculateGrade(80));
        $this->assertEquals('C', $this->calculateGrade(75));
        $this->assertEquals('C', $this->calculateGrade(70));
        $this->assertEquals('D', $this->calculateGrade(65));
        $this->assertEquals('D', $this->calculateGrade(60));
        $this->assertEquals('F', $this->calculateGrade(55));
        $this->assertEquals('F', $this->calculateGrade(0));
    }

    public function test_grade_calculation_edge_cases()
    {
        $this->assertEquals('A', $this->calculateGrade(100));
        $this->assertEquals('F', $this->calculateGrade(-10));
        $this->assertEquals('F', $this->calculateGrade(59.9));
        $this->assertEquals('D', $this->calculateGrade(60.0));
    }

    /**
     * Test pass/fail determination
     */
    public function test_pass_fail_determination()
    {
        $passingPercentage = 40.0;

        $this->assertTrue(50.0 >= $passingPercentage, 'Score 50% should pass');
        $this->assertTrue(40.0 >= $passingPercentage, 'Score 40% should pass');
        $this->assertFalse(39.0 >= $passingPercentage, 'Score 39% should fail');
        $this->assertFalse(0.0 >= $passingPercentage, 'Score 0% should fail');
    }

    /**
     * Test time remaining calculation
     */
    public function test_time_remaining_calculation()
    {
        $startTime = strtotime('2024-01-01 10:00:00');
        $currentTime = strtotime('2024-01-01 10:15:00');
        $duration = 3600; // 60 minutes

        $elapsed = $currentTime - $startTime; // 15 minutes = 900 seconds
        $remaining = $duration - $elapsed; // 45 minutes = 2700 seconds

        $this->assertEquals(2700, $remaining);
        $this->assertEquals(45, $remaining / 60); // 45 minutes
    }

    public function test_time_remaining_with_expired_time()
    {
        $startTime = strtotime('2024-01-01 10:00:00');
        $currentTime = strtotime('2024-01-01 11:30:00');
        $duration = 3600; // 60 minutes

        $elapsed = $currentTime - $startTime; // 90 minutes = 5400 seconds
        $remaining = $duration - $elapsed; // -30 minutes = -1800 seconds

        $this->assertEquals(-1800, $remaining);
        $this->assertLessThan(0, $remaining);
    }

    /**
     * Test string validation
     */
    public function test_string_length_validation()
    {
        $this->assertTrue($this->isValidLength('Hello', 5, 10));
        $this->assertTrue($this->isValidLength('Hello World', 5, 15));
        $this->assertFalse($this->isValidLength('Hi', 5, 10));
        $this->assertFalse($this->isValidLength('This is too long', 5, 10));
    }

    public function test_string_contains_only_letters()
    {
        $this->assertTrue($this->containsOnlyLetters('Hello'));
        $this->assertTrue($this->containsOnlyLetters('HelloWorld'));
        $this->assertFalse($this->containsOnlyLetters('Hello123'));
        $this->assertFalse($this->containsOnlyLetters('Hello World'));
        $this->assertFalse($this->containsOnlyLetters('Hello-World'));
    }

    /**
     * Helper methods
     */
    private function calculatePercentage($obtained, $total): float
    {
        if ($total == 0) {
            return 0.0;
        }
        return ($obtained / $total) * 100;
    }

    private function formatTime($seconds): string
    {
        if ($seconds < 60) {
            return $seconds == 1 ? '1 second' : $seconds . ' seconds';
        } elseif ($seconds < 3600) {
            $minutes = floor($seconds / 60);
            $secs = $seconds % 60;
            if ($secs == 0) {
                return $minutes == 1 ? '1 minute' : $minutes . ' minutes';
            }
            return "{$minutes}m {$secs}s";
        } else {
            $hours = floor($seconds / 3600);
            $minutes = floor(($seconds % 3600) / 60);
            $secs = $seconds % 60;
            $result = "{$hours}h";
            if ($minutes > 0) $result .= " {$minutes}m";
            if ($secs > 0) $result .= " {$secs}s";
            return $result;
        }
    }

    private function calculateGrade(float $percentage): string
    {
        if ($percentage >= 90) return 'A';
        if ($percentage >= 80) return 'B';
        if ($percentage >= 70) return 'C';
        if ($percentage >= 60) return 'D';
        return 'F';
    }

    private function isStrongPassword(string $password): bool
    {
        return strlen($password) >= 8 &&
               preg_match('/[A-Z]/', $password) &&
               preg_match('/[a-z]/', $password) &&
               preg_match('/[0-9]/', $password) &&
               preg_match('/[^A-Za-z0-9]/', $password);
    }

    private function isValidLength(string $string, int $min, int $max): bool
    {
        $length = strlen($string);
        return $length >= $min && $length <= $max;
    }

    private function containsOnlyLetters(string $string): bool
    {
        return ctype_alpha($string);
    }
}
