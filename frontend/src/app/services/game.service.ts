import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class GameService {
  private apiUrl = 'http://localhost:8080/api/games'; 

  constructor(private http: HttpClient) {}

  getGames(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  addGame(game: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, game);
  }

  deleteGame(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  }
}