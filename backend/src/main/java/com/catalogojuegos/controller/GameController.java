package com.catalogojuegos.controller;

import com.catalogojuegos.model.Game;
import com.catalogojuegos.repository.GameRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "*", methods = {RequestMethod.GET, RequestMethod.POST, RequestMethod.DELETE, RequestMethod.PUT})
@RestController
@RequestMapping("/api/games")
public class GameController {

    @Autowired
    private GameRepository repository;

    @GetMapping
    public List<Game> getAll() {
        return repository.findAll();
    }

    @PostMapping
    public Game create(@RequestBody Game game) {
        return repository.save(game);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        repository.deleteById(id);
    }
}