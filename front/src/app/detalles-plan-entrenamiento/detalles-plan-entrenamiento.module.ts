import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; 
import { FormsModule } from '@angular/forms';
import { DetallesPlanEntrenamientoComponent } from './detalles-plan-entrenamiento.component';
import { DetallesPlanEntrenamientoService } from './detalles-plan-entrenamiento.service';
import { TrainingPlan } from './training-plan.model';


@NgModule({
  imports: [
    CommonModule,RouterModule, FormsModule
  ],
  exports: [
    DetallesPlanEntrenamientoComponent
  ],
  declarations: [
    DetallesPlanEntrenamientoComponent
  ],
  providers: [
    DetallesPlanEntrenamientoService
  ]
})
export class DetallesPlanEntrenamientoModule { }