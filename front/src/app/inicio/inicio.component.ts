import { Component, OnInit } from '@angular/core';
import { InicioService } from './inicio.service';
import { Ejercicio } from '../detalles-ejercicio/ejercicio.model';
import { TrainingPlan } from '../detalles-plan-entrenamiento/training-plan.model';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-inicio',
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.css']
})
export class InicioComponent implements OnInit {
  
  ejercicios$: Observable<any[]> | undefined;
  planEntrenamiento?: TrainingPlan;
  planEntrenamientoId: number = 1; // ID del plan de entrenamiento que deseas obtener

  constructor(private inicioService: InicioService, private router: Router) { }

  ngOnInit() {
    
    this.ejercicios$ = this.inicioService.obtenerEjercicios();
    console.log(this.ejercicios$)
    const token = sessionStorage.getItem('token');
     if (!token) {
       // Si el token no está presente, redirigir al usuario al login
       this.router.navigate(['/login']);
       return;
     }
     const rol = sessionStorage.getItem('rol');
     console.log('Rol del usuario:', rol);
     
  }

  /*obtenerEjercicioPorId(id: number) {
    this.inicioService.obtenerEjercicioPorId(id).subscribe(
      (ejercicio: Ejercicio) => this.ejercicio = ejercicio,
      (error: any) => console.error('Error al obtener el ejercicio', error)
    );
  }*/

  /*obtenerEjercicios(): void {
    this.inicioService.obtenerEjercicios().subscribe(
      (data: any[]) => {
        this.ejercicios = data;
        console.log(this.ejercicios)
      },
      (error: any) => {
        console.error('Error al obtener los ejercicios', error);
      }
    );
  }*/

  /*obtenerPlanEntrenamientoPorId(id: number) {
    this.inicioService.obtenerPlanEntrenamientoPorId(id).subscribe(
      (plan: TrainingPlan) => this.planEntrenamiento = plan,
      (error: any) => console.error('Error al obtener el plan de entrenamiento', error)
    );
  }*/
  
  
}
