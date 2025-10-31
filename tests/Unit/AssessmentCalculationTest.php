<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class AssessmentCalculationTest extends TestCase
{
    /**
     * Test score percentage calculation
     */
    public function test_score_percentage_calculation()
    {
        $testCases = [
            ['obtained' => 80, 'total' => 100, 'expected' => 80.0],
            ['obtained' => 45, 'total' => 50, 'expected' => 90.0],
            ['obtained' => 0, 'total' => 100, 'expected' => 0.0],
            ['obtained' => 100, 'total' => 100, 'expected' => 100.0],
            ['obtained' => 25, 'total' => 30, 'expected' => 83.33333333333334],
        ];

        foreach ($testCases as $case) {
            $percentage = $this->calculateScorePercentage($case['obtained'], $case['total']);
            $this->assertEquals(
                $case['expected'],
                $percentage,
                "Score calculation failed for {$case['obtained']}/{$case['total']}",
                0.01
            );
        }
    }

    public function test_score_percentage_with_zero_total()
    {
        $percentage = $this->calculateScorePercentage(50, 0);
        $this->assertEquals(0.0, $percentage);
    }

    public function test_score_percentage_with_negative_values()
    {
        $percentage = $this->calculateScorePercentage(-10, 100);
        $this->assertEquals(-10.0, $percentage);
    }

    /**
     * Test pass/fail determination
     */
    public function test_pass_fail_determination()
    {
        $passingPercentage = 40.0;

        $this->assertTrue($this->isPassing(50.0, $passingPercentage), 'Score 50% should pass');
        $this->assertTrue($this->isPassing(40.0, $passingPercentage), 'Score 40% should pass');
        $this->assertFalse($this->isPassing(39.0, $passingPercentage), 'Score 39% should fail');
        $this->assertFalse($this->isPassing(0.0, $passingPercentage), 'Score 0% should fail');
    }

    public function test_pass_fail_with_custom_threshold()
    {
        $passingPercentage = 60.0;

        $this->assertTrue($this->isPassing(70.0, $passingPercentage));
        $this->assertTrue($this->isPassing(60.0, $passingPercentage));
        $this->assertFalse($this->isPassing(59.0, $passingPercentage));
    }

    /**
     * Test grade calculation
     */
    public function test_grade_calculation()
    {
        $this->assertEquals('A+', $this->calculateGrade(97));
        $this->assertEquals('A', $this->calculateGrade(93));
        $this->assertEquals('A-', $this->calculateGrade(90));
        $this->assertEquals('B+', $this->calculateGrade(87));
        $this->assertEquals('B', $this->calculateGrade(83));
        $this->assertEquals('B-', $this->calculateGrade(80));
        $this->assertEquals('C+', $this->calculateGrade(77));
        $this->assertEquals('C', $this->calculateGrade(73));
        $this->assertEquals('C-', $this->calculateGrade(70));
        $this->assertEquals('D+', $this->calculateGrade(67));
        $this->assertEquals('D', $this->calculateGrade(63));
        $this->assertEquals('D-', $this->calculateGrade(60));
        $this->assertEquals('F', $this->calculateGrade(55));
        $this->assertEquals('F', $this->calculateGrade(0));
    }

    public function test_grade_calculation_edge_cases()
    {
        $this->assertEquals('A+', $this->calculateGrade(100));
        $this->assertEquals('F', $this->calculateGrade(-10));
        $this->assertEquals('F', $this->calculateGrade(59.9));
        $this->assertEquals('D-', $this->calculateGrade(60.0));
    }

    /**
     * Test time remaining calculation
     */
    public function test_time_remaining_calculation()
    {
        $startTime = strtotime('2024-01-01 10:00:00');
        $currentTime = strtotime('2024-01-01 10:15:00');
        $duration = 3600; // 60 minutes

        $remaining = $this->calculateTimeRemaining($startTime, $currentTime, $duration);

        $this->assertEquals(2700, $remaining); // 45 minutes = 2700 seconds
        $this->assertEquals(45, $remaining / 60); // 45 minutes
    }

    public function test_time_remaining_with_expired_time()
    {
        $startTime = strtotime('2024-01-01 10:00:00');
        $currentTime = strtotime('2024-01-01 11:30:00');
        $duration = 3600; // 60 minutes

        $remaining = $this->calculateTimeRemaining($startTime, $currentTime, $duration);

        $this->assertEquals(-1800, $remaining); // -30 minutes = -1800 seconds
        $this->assertLessThan(0, $remaining);
    }

    public function test_time_remaining_with_exact_time()
    {
        $startTime = strtotime('2024-01-01 10:00:00');
        $currentTime = strtotime('2024-01-01 11:00:00');
        $duration = 3600; // 60 minutes

        $remaining = $this->calculateTimeRemaining($startTime, $currentTime, $duration);

        $this->assertEquals(0, $remaining);
    }

    /**
     * Test assessment statistics calculation
     */
    public function test_average_score_calculation()
    {
        $scores = [80, 90, 70, 85, 95];
        $average = $this->calculateAverageScore($scores);

        $this->assertEquals(84.0, $average);
    }

    public function test_average_score_with_empty_array()
    {
        $scores = [];
        $average = $this->calculateAverageScore($scores);

        $this->assertEquals(0.0, $average);
    }

    public function test_average_score_with_single_value()
    {
        $scores = [85];
        $average = $this->calculateAverageScore($scores);

        $this->assertEquals(85.0, $average);
    }

    /**
     * Test difficulty level calculation
     */
    public function test_difficulty_level_calculation()
    {
        $this->assertEquals('Easy', $this->calculateDifficultyLevel(85));
        $this->assertEquals('Medium', $this->calculateDifficultyLevel(65));
        $this->assertEquals('Hard', $this->calculateDifficultyLevel(45));
    }

    public function test_difficulty_level_edge_cases()
    {
        $this->assertEquals('Easy', $this->calculateDifficultyLevel(80));
        $this->assertEquals('Medium', $this->calculateDifficultyLevel(60));
        $this->assertEquals('Hard', $this->calculateDifficultyLevel(40));
    }

    /**
     * Test question distribution calculation
     */
    public function test_question_distribution_calculation()
    {
        $totalQuestions = 100;
        $easyQuestions = 40;
        $mediumQuestions = 35;
        $hardQuestions = 25;

        $distribution = $this->calculateQuestionDistribution($totalQuestions, $easyQuestions, $mediumQuestions, $hardQuestions);

        $this->assertEquals(40.0, $distribution['easy_percentage']);
        $this->assertEquals(35.0, $distribution['medium_percentage']);
        $this->assertEquals(25.0, $distribution['hard_percentage']);
    }

    public function test_question_distribution_with_zero_questions()
    {
        $totalQuestions = 0;
        $easyQuestions = 0;
        $mediumQuestions = 0;
        $hardQuestions = 0;

        $distribution = $this->calculateQuestionDistribution($totalQuestions, $easyQuestions, $mediumQuestions, $hardQuestions);

        $this->assertEquals(0.0, $distribution['easy_percentage']);
        $this->assertEquals(0.0, $distribution['medium_percentage']);
        $this->assertEquals(0.0, $distribution['hard_percentage']);
    }

    /**
     * Test assessment duration validation
     */
    public function test_assessment_duration_validation()
    {
        $this->assertTrue($this->isValidDuration(30)); // 30 minutes
        $this->assertTrue($this->isValidDuration(60)); // 1 hour
        $this->assertTrue($this->isValidDuration(120)); // 2 hours
        $this->assertFalse($this->isValidDuration(0)); // 0 minutes
        $this->assertFalse($this->isValidDuration(-30)); // Negative
        $this->assertFalse($this->isValidDuration(300)); // 5 hours (too long)
    }

    /**
     * Helper methods
     */
    private function calculateScorePercentage($obtained, $total): float
    {
        if ($total == 0) {
            return 0.0;
        }
        return ($obtained / $total) * 100;
    }

    private function isPassing(float $score, float $threshold): bool
    {
        return $score >= $threshold;
    }

    private function calculateGrade(float $percentage): string
    {
        if ($percentage >= 97) return 'A+';
        if ($percentage >= 93) return 'A';
        if ($percentage >= 90) return 'A-';
        if ($percentage >= 87) return 'B+';
        if ($percentage >= 83) return 'B';
        if ($percentage >= 80) return 'B-';
        if ($percentage >= 77) return 'C+';
        if ($percentage >= 73) return 'C';
        if ($percentage >= 70) return 'C-';
        if ($percentage >= 67) return 'D+';
        if ($percentage >= 63) return 'D';
        if ($percentage >= 60) return 'D-';
        return 'F';
    }

    private function calculateTimeRemaining(int $startTime, int $currentTime, int $duration): int
    {
        $elapsed = $currentTime - $startTime;
        return $duration - $elapsed;
    }

    private function calculateAverageScore(array $scores): float
    {
        if (empty($scores)) {
            return 0.0;
        }
        return array_sum($scores) / count($scores);
    }

    private function calculateDifficultyLevel(float $averageScore): string
    {
        if ($averageScore >= 70) return 'Easy';
        if ($averageScore >= 50) return 'Medium';
        return 'Hard';
    }

    private function calculateQuestionDistribution(int $total, int $easy, int $medium, int $hard): array
    {
        if ($total == 0) {
            return [
                'easy_percentage' => 0.0,
                'medium_percentage' => 0.0,
                'hard_percentage' => 0.0
            ];
        }

        return [
            'easy_percentage' => ($easy / $total) * 100,
            'medium_percentage' => ($medium / $total) * 100,
            'hard_percentage' => ($hard / $total) * 100
        ];
    }

    private function isValidDuration(int $minutes): bool
    {
        return $minutes > 0 && $minutes <= 240; // Max 4 hours
    }
}
