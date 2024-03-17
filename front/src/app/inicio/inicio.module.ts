import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; // Importa RouterModule si vas a usar rutas
import { InicioComponent } from './inicio.component';
import { InicioService } from './inicio.service';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    InicioComponent
  ],
  imports: [
    CommonModule,
    RouterModule, FormsModule
  ],
  providers: [
    InicioService
  ],
  exports: [
    InicioComponent
  ]
})
export class InicioModule { }