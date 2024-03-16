import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UsuarioLoginComponent } from './usuario/usuario-login/usuario-login.component';
import { UsuarioRegistroComponent } from './usuario/usuario-registro/usuario-registro.component';
import { DetallesEjercicioComponent } from './detalles-ejercicio/detalles-ejercicio.component';
import { DetallesPlanEntrenamientoComponent } from './detalles-plan-entrenamiento/detalles-plan-entrenamiento.component';
import { InicioComponent } from './inicio/inicio.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: UsuarioLoginComponent },
  { path: 'registro', component: UsuarioRegistroComponent },
  {
    path: 'inicio', // Ruta padre para la página de inicio
    component: InicioComponent,
    children: [
      { path: 'detalles-ejercicio/:id', component: DetallesEjercicioComponent }, // Ruta hija para detalles de ejercicio
      { path: 'detalles-plan-entrenamiento', component: DetallesPlanEntrenamientoComponent } // Ruta hija para detalles del plan de entrenamiento
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }