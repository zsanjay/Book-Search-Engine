package com.library.repository;

import com.library.entity.Book;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import java.util.List;
import static org.assertj.core.api.Assertions.assertThat;


@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class BookRepositoryTest {

    @Autowired
    private BookRepository bookRepository;

    @Test
    @DisplayName("searchBooks should return books matching the search term")
    void testSearchBooks() {
        // When
        List<Book> results = bookRepository.searchBooks("algorithms");

        // Then
        assertThat(results).isNotNull();
        assertThat(results).anyMatch(book -> book.getTitle().toLowerCase().contains("algorithms"));
    }
}