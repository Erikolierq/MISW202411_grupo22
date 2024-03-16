import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component'; 
import { CommonModule } from '@angular/common';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { UsuarioModule } from './usuario/usuario.module';
import { ToastrModule } from 'ngx-toastr';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { DetallesEjercicioModule } from './detalles-ejercicio/detalles-ejercicio.module';
import { InicioComponent } from './inicio/inicio.component';
import { TrainingSessionComponent } from './TrainingSession/TrainingSession.component';
import { NotificationComponentComponent } from './NotificationComponent/NotificationComponent.component';
import { DetallesPlanEntrenamientoModule } from './detalles-plan-entrenamiento/detalles-plan-entrenamiento.module';
import { InicioModule } from './inicio/inicio.module';


@NgModule({
  declarations: [											
    AppComponent,

   ],
  imports: [
    BrowserModule,
    UsuarioModule,
    DetallesEjercicioModule,
    DetallesPlanEntrenamientoModule, 
    InicioModule,
    FormsModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    CommonModule,
    ToastrModule.forRoot({
      timeOut: 7000,
      positionClass: 'toast-bottom-right',
      preventDuplicates: true,
    }),
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }