import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Ejercicio } from '../detalles-ejercicio/ejercicio.model'; 
import { environment } from '../../environments/environment'; // Ajusta esta ruta si es necesario
import { TrainingPlan } from '../detalles-plan-entrenamiento/training-plan.model';

@Injectable({
  providedIn: 'root'
})
export class InicioService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Método para obtener un ejercicio aleatorio o por algún criterio específico
  /*obtenerEjercicioAleatorio(): Observable<Ejercicio> {
    // Este endpoint debe ajustarse a lo que tu API soporte para obtener un ejercicio aleatorio
    return this.http.get<Ejercicio>(`${this.apiUrl}/ejercicio/aleatorio`);
  }

  obtenerEjercicioPorId(id: number): Observable<Ejercicio> {
    return this.http.get<Ejercicio>(`${this.apiUrl}/ejercicio/${id}`);
  }*/
  
  obtenerEjercicios(): Observable<any[]> {
    // De nuevo, este endpoint se debe ajustar a tu API para obtener todos los ejercicios
    return this.http.get<any[]>(`${this.apiUrl}/ejercicios`);
  }
  
  /*obtenerPlanEntrenamientoPorId(id: number): Observable<TrainingPlan> {
    return this.http.get<TrainingPlan>(`${this.apiUrl}/plan-entrenamiento/${id}`);
  }*/

  // Si necesitas enviar un token de autorización, puedes obtenerlo de sessionStorage como en UsuarioService
  private getHeaders(): HttpHeaders {
    return new HttpHeaders({
      Authorization: `Bearer ${sessionStorage.getItem('token')}`,
    });
  }
}