import { Component, OnInit } from '@angular/core';
import { InicioService } from './inicio.service';
import { Ejercicio } from '../detalles-ejercicio/ejercicio.model';
import { TrainingPlan } from '../detalles-plan-entrenamiento/training-plan.model';

@Component({
  selector: 'app-inicio',
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.css']
})
export class InicioComponent implements OnInit {
  ejercicio?: Ejercicio;
  ejercicios?: Ejercicio[];
  planEntrenamiento?: TrainingPlan;
  ejercicioId: number = 1; // ID del ejercicio que deseas obtener
  planEntrenamientoId: number = 1; // ID del plan de entrenamiento que deseas obtener

  constructor(private inicioService: InicioService) { }

  ngOnInit() {
    this.obtenerEjercicioPorId(this.ejercicioId);
    this.obtenerEjercicios(); // Si aún deseas obtener todos los ejercicios
    this.obtenerPlanEntrenamientoPorId(this.planEntrenamientoId);
  }

  obtenerEjercicioPorId(id: number) {
    this.inicioService.obtenerEjercicioPorId(id).subscribe(
      (ejercicio: Ejercicio) => this.ejercicio = ejercicio,
      (error: any) => console.error('Error al obtener el ejercicio', error)
    );
  }

  obtenerEjercicios() {
    this.inicioService.obtenerEjercicios().subscribe(
      (ejercicios: Ejercicio[]) => this.ejercicios = ejercicios,
      (error: any) => console.error('Error al obtener los ejercicios', error)
    );
  }

  obtenerPlanEntrenamientoPorId(id: number) {
    this.inicioService.obtenerPlanEntrenamientoPorId(id).subscribe(
      (plan: TrainingPlan) => this.planEntrenamiento = plan,
      (error: any) => console.error('Error al obtener el plan de entrenamiento', error)
    );
  }
}
