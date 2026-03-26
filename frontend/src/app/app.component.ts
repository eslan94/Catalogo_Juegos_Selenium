import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GameService } from './services/game.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  isLoggedIn = false;
  juegos: any[] = [];
  
  usuario = { username: '', password: '' };
  
  // Modelo inicializado para evitar valores nulos
  nuevoJuego = { 
    title: '', 
    platform: '', 
    genre: '', 
    imageUrl: '', 
    hoursPlayed: 0, 
    rating: 5 
  };

  private credencialesValidas = [
    { user: 'esteban_pro', pass: 'clave123' },
    { user: 'admin', pass: 'admin456' }
  ];

  constructor(private gameService: GameService) {}

  ngOnInit() {
    if (this.isLoggedIn) {
      this.cargarJuegos();
    }
  }

  login() {
    const validado = this.credencialesValidas.find(
      c => c.user === this.usuario.username && c.pass === this.usuario.password
    );

    if (validado) {
      this.isLoggedIn = true;
      this.cargarJuegos();
      console.log("Acceso concedido");
    } else {
      alert("Validation failed: Credenciales incorrectas");
    }
  }

  logout() {
    this.isLoggedIn = false;
    this.usuario = { username: '', password: '' };
  }

  cargarJuegos() {
    this.gameService.getGames().subscribe(data => {
      this.juegos = data;
    });
  }

  registrar() {
    this.gameService.addGame(this.nuevoJuego).subscribe(() => {
      this.cargarJuegos(); 
      this.nuevoJuego = { title: '', platform: '', genre: '', imageUrl: '', hoursPlayed: 0, rating: 5 };
    });
  }

  eliminar(id: number) {
  // Confirmación profesional
    if (confirm('¿Estás seguro de eliminar este juego del inventario?')) {
      this.gameService.deleteGame(id).subscribe(() => {
        this.cargarJuegos(); // Refresca la galería
      });
    }
  }

  // Métodos para renderizar exactamente 5 estrellas
  getStars(rating: number): number[] {
    const filled = Math.max(0, Math.min(5, Math.floor(rating || 0)));
    return Array(filled).fill(0);
  }

  getEmptyStars(rating: number): number[] {
    const filled = Math.max(0, Math.min(5, Math.floor(rating || 0)));
    const empty = 5 - filled;
    return Array(empty).fill(0);
  }
}