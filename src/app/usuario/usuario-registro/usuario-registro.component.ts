import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { UsuarioService } from '../usuario.service';
import { Usuario } from '../usuario';

@Component({
  selector: 'app-usuario-registro',
  templateUrl: './usuario-registro.component.html',
  styleUrls: ['./usuario-registro.component.css'],
})
export class UsuarioRegistroComponent implements OnInit {
  usuarioForm!: FormGroup;
  listaRoles = ['deportista', 'instructor', 'medico_deportologo', 'administrador'];

  constructor(
    private usuarioService: UsuarioService,
    private formBuilder: FormBuilder,
    private router: Router,
    private toastrService: ToastrService
  ) {}

  ngOnInit() {
    this.usuarioForm = this.formBuilder.group({
      usuario: ['', [Validators.required, Validators.maxLength(50)]],
      correo: ['', [Validators.required, Validators.email]],
      contrasena: ['', [Validators.required, Validators.minLength(4), Validators.maxLength(50)]],
      confirmPassword: ['', [Validators.required]],
      rol: ['', [Validators.required]],
      nombre: ['', Validators.maxLength(50)],  // Opcional
      numeroContacto: ['', Validators.maxLength(50)]  // Opcional
    }, { validator: this.mustMatch('contrasena', 'confirmPassword') });
  }

  registrarUsuario() {
    if (this.usuarioForm.valid) {
      const nuevoUsuario = new Usuario(
        0, // ID será generado por el backend o la base de datos
        this.usuarioForm.value.usuario,
        this.usuarioForm.value.contrasena,
        this.usuarioForm.value.rol,
        this.usuarioForm.value.correo,
        this.usuarioForm.value.nombre,
        this.usuarioForm.value.numeroContacto
      );
      this.usuarioService.registro(nuevoUsuario).subscribe(
        res => {
          this.toastrService.success("Registro exitoso", "Información", { closeButton: true });
          this.router.navigate(['/login']); // Asegúrate de que esta es la ruta correcta
        },
        error => {
          this.toastrService.error("Error en el registro", "Error", { closeButton: true });
        }
      );
    } else {
      this.toastrService.error("Por favor, verifica que los datos del formulario sean correctos y que las contraseñas coincidan.", "Error en el formulario", { closeButton: true });
    }
  }

  mustMatch(password: string, confirmPassword: string) {
    return (formGroup: FormGroup) => {
      const passwordControl = formGroup.controls[password];
      const confirmPasswordControl = formGroup.controls[confirmPassword];

      if (passwordControl.value !== confirmPasswordControl.value) {
        confirmPasswordControl.setErrors({ mustMatch: true });
      } else {
        confirmPasswordControl.setErrors(null);
      }
    }
  }
}
