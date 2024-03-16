import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UsuarioLoginComponent } from './usuario-login/usuario-login.component';
import { UsuarioRegistroComponent } from './usuario-registro/usuario-registro.component';

@NgModule({
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  exports: [UsuarioLoginComponent, UsuarioRegistroComponent],
  declarations: [UsuarioLoginComponent, UsuarioRegistroComponent],
})
export class UsuarioModule {}
