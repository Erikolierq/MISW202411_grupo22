import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Ejercicio } from './ejercicio.model';
import { EjercicioService } from './ejercicio.service';
import { ToastrService } from 'ngx-toastr';
import { Subscription, throwError } from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Component({
  selector: 'app-detalles-ejercicio',
  templateUrl: './detalles-ejercicio.component.html',
  styleUrls: ['./detalles-ejercicio.component.css']
})
export class DetallesEjercicioComponent implements OnInit, OnDestroy {
  ejercicio: Ejercicio | null = null;
  loading = true;
  ejercicioSubscription: Subscription = new Subscription();

  constructor(
    private ejercicioService: EjercicioService,
    private route: ActivatedRoute,
    private toastr: ToastrService
  ) { }

  ngOnInit(): void {
    this.ejercicioSubscription = this.route.paramMap.pipe(
      switchMap(params => {
        const idParam = params.get('id');
        if (idParam !== null) { // Comprobación de nulidad
          const id = +idParam;
          return this.ejercicioService.getEjercicioById(id);
        }
        // Puedes manejar el caso en que el parámetro 'id' es nulo, si es necesario
        return throwError('El ID del ejercicio es nulo');
      })
    ).subscribe(
      (ejercicio: Ejercicio) => {
        this.ejercicio = ejercicio;
        this.loading = false;
      },
      (error) => {
        console.error('Error fetching ejercicio:', error);
        this.toastr.error(error.error?.mensaje ?? 'Ocurrió un error al cargar el ejercicio');
        this.loading = false;
      }
    );
  }

  ngOnDestroy(): void {
    this.ejercicioSubscription.unsubscribe();
  }

  isEjercicioNotNull(): boolean {
    return this.ejercicio !== null;
  }
}
