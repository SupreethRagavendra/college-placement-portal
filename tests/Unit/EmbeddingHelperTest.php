<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use App\Services\EmbeddingHelper;

class EmbeddingHelperTest extends TestCase
{
    protected $embeddingHelper;

    protected function setUp(): void
    {
        parent::setUp();
        $this->embeddingHelper = new EmbeddingHelper();
    }

    /**
     * Test cosine similarity calculation
     */
    public function test_cosine_similarity_with_identical_vectors()
    {
        $vector1 = [1.0, 2.0, 3.0];
        $vector2 = [1.0, 2.0, 3.0];
        
        $similarity = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        
        // Identical vectors should have similarity of 1.0
        $this->assertEquals(1.0, $similarity, '', 0.0001);
    }

    public function test_cosine_similarity_with_opposite_vectors()
    {
        $vector1 = [1.0, 0.0, 0.0];
        $vector2 = [-1.0, 0.0, 0.0];
        
        $similarity = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        
        // Opposite vectors should have similarity of -1.0
        $this->assertEquals(-1.0, $similarity, '', 0.0001);
    }

    public function test_cosine_similarity_with_orthogonal_vectors()
    {
        $vector1 = [1.0, 0.0, 0.0];
        $vector2 = [0.0, 1.0, 0.0];
        
        $similarity = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        
        // Orthogonal vectors should have similarity of 0.0
        $this->assertEquals(0.0, $similarity, '', 0.0001);
    }

    public function test_cosine_similarity_with_different_length_vectors()
    {
        $vector1 = [1.0, 2.0];
        $vector2 = [1.0, 2.0, 3.0];
        
        $similarity = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        
        // Different length vectors should return 0.0
        $this->assertEquals(0.0, $similarity);
    }

    public function test_cosine_similarity_with_zero_vectors()
    {
        $vector1 = [0.0, 0.0, 0.0];
        $vector2 = [1.0, 2.0, 3.0];
        
        $similarity = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        
        // Zero vector should return 0.0
        $this->assertEquals(0.0, $similarity);
    }

    public function test_cosine_similarity_with_partial_similarity()
    {
        $vector1 = [1.0, 1.0, 0.0];
        $vector2 = [1.0, 0.0, 0.0];
        
        $similarity = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        
        // Should have positive similarity but less than 1.0
        $this->assertGreaterThan(0.0, $similarity);
        $this->assertLessThan(1.0, $similarity);
    }

    /**
     * Test vector normalization
     */
    public function test_normalize_embedding_produces_unit_vector()
    {
        $vector = [3.0, 4.0]; // Magnitude = 5
        
        $normalized = $this->embeddingHelper->normalizeEmbedding($vector);
        
        // Calculate magnitude of normalized vector
        $magnitude = sqrt($normalized[0]**2 + $normalized[1]**2);
        
        // Normalized vector should have magnitude of 1.0
        $this->assertEquals(1.0, $magnitude, '', 0.0001);
        $this->assertEquals(0.6, $normalized[0], '', 0.0001); // 3/5
        $this->assertEquals(0.8, $normalized[1], '', 0.0001); // 4/5
    }

    public function test_normalize_embedding_with_zero_vector()
    {
        $vector = [0.0, 0.0, 0.0];
        
        $normalized = $this->embeddingHelper->normalizeEmbedding($vector);
        
        // Zero vector should remain zero after normalization
        $this->assertEquals([0.0, 0.0, 0.0], $normalized);
    }

    public function test_normalize_embedding_with_negative_values()
    {
        $vector = [-3.0, -4.0]; // Magnitude = 5
        
        $normalized = $this->embeddingHelper->normalizeEmbedding($vector);
        
        // Calculate magnitude of normalized vector
        $magnitude = sqrt($normalized[0]**2 + $normalized[1]**2);
        
        // Normalized vector should have magnitude of 1.0
        $this->assertEquals(1.0, $magnitude, '', 0.0001);
        $this->assertEquals(-0.6, $normalized[0], '', 0.0001); // -3/5
        $this->assertEquals(-0.8, $normalized[1], '', 0.0001); // -4/5
    }

    public function test_normalize_embedding_with_single_element()
    {
        $vector = [5.0];
        
        $normalized = $this->embeddingHelper->normalizeEmbedding($vector);
        
        // Single element vector should normalize to [1.0]
        $this->assertEquals([1.0], $normalized);
    }

    /**
     * Test edge cases
     */
    public function test_cosine_similarity_with_empty_vectors()
    {
        $vector1 = [];
        $vector2 = [];
        
        $similarity = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        
        // Empty vectors should return 0.0
        $this->assertEquals(0.0, $similarity);
    }

    public function test_cosine_similarity_with_one_empty_vector()
    {
        $vector1 = [1.0, 2.0];
        $vector2 = [];
        
        $similarity = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        
        // One empty vector should return 0.0
        $this->assertEquals(0.0, $similarity);
    }

    public function test_normalize_embedding_with_empty_vector()
    {
        $vector = [];
        
        $normalized = $this->embeddingHelper->normalizeEmbedding($vector);
        
        // Empty vector should remain empty
        $this->assertEquals([], $normalized);
    }

    /**
     * Test mathematical properties
     */
    public function test_cosine_similarity_symmetry()
    {
        $vector1 = [1.0, 2.0, 3.0];
        $vector2 = [4.0, 5.0, 6.0];
        
        $similarity1 = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        $similarity2 = $this->embeddingHelper->cosineSimilarity($vector2, $vector1);
        
        // Cosine similarity should be symmetric
        $this->assertEquals($similarity1, $similarity2, '', 0.0001);
    }

    public function test_cosine_similarity_range()
    {
        $vector1 = [1.0, 2.0, 3.0];
        $vector2 = [4.0, 5.0, 6.0];
        
        $similarity = $this->embeddingHelper->cosineSimilarity($vector1, $vector2);
        
        // Cosine similarity should be between -1 and 1
        $this->assertGreaterThanOrEqual(-1.0, $similarity);
        $this->assertLessThanOrEqual(1.0, $similarity);
    }
}
