import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DetallesEjercicioComponent } from './detalles-ejercicio.component';
import { EjercicioService } from './ejercicio.service'; // Asumiendo que tienes un servicio EjercicioService
import { RouterModule } from '@angular/router'; // Importar RouterModule si vas a utilizar rutas en este módulo
import { FormsModule } from '@angular/forms';

@NgModule({
  imports: [
    CommonModule,RouterModule, FormsModule
  ],
  exports: [
    DetallesEjercicioComponent
  ],
  declarations: [
    DetallesEjercicioComponent
  ],
  providers: [
    EjercicioService
  ]
})
export class DetallesEjercicioModule { }