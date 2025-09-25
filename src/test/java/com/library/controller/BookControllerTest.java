package com.library.controller;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.ResponseEntity;

import com.library.entity.Book;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class BookControllerTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void testSearchBooks() {
        String searchTerm = "algorithms";
        String url = "/books/search?searchTerm={searchTerm}";
        ResponseEntity<Book[]> response = restTemplate.getForEntity(url, Book[].class, searchTerm);

        Book[] books = response.getBody();
        assertNotNull(books);
        assertTrue(books.length > 0);

        for (Book book : books) {
            System.out.println(book);
        }
    }
}
