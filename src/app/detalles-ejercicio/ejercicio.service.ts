import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ejercicio } from './ejercicio.model';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class EjercicioService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getEjercicioById(ejercicioId: number): Observable<Ejercicio> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${sessionStorage.getItem('token')}`,
    });
    return this.http.get<Ejercicio>(`${this.apiUrl}/exercises/${ejercicioId}`, { headers: headers });
  }

  crearEjercicio(ejercicio: Ejercicio): Observable<Ejercicio> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${sessionStorage.getItem('token')}`,
    });
    return this.http.post<Ejercicio>(`${this.apiUrl}/exercises`, ejercicio, { headers: headers });
  }

  actualizarEjercicio(ejercicioId: number, ejercicio: Ejercicio): Observable<Ejercicio> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${sessionStorage.getItem('token')}`,
    });
    return this.http.put<Ejercicio>(`${this.apiUrl}/exercises/${ejercicioId}`, ejercicio, { headers: headers });
  }

  eliminarEjercicio(ejercicioId: number): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${sessionStorage.getItem('token')}`,
    });
    return this.http.delete<any>(`${this.apiUrl}/exercises/${ejercicioId}`, { headers: headers });
  }
}