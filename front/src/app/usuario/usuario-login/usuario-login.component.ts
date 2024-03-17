import { Component, OnInit } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { UsuarioService } from '../usuario.service';

@Component({
  selector: 'app-usuario-login',
  templateUrl: './usuario-login.component.html',
  styleUrls: ['./usuario-login.component.css']
})
export class UsuarioLoginComponent implements OnInit {
  usuario: string = '';
  contrasena: string = '';
  correo: string = '';
  password: string = '';
  error: string = '';
  helper = new JwtHelperService();

  constructor(
    private usuarioService: UsuarioService,
    private toastrService: ToastrService,
    private router: Router
  ) { }

  ngOnInit() {
    sessionStorage.clear();
  }

  loginUsuario(usuario: string, contrasena: string) {
    this.error = '';
  
    this.usuarioService.login(usuario, contrasena)
      .subscribe(res => {
        const decodedToken = this.helper.decodeToken(res.token);
        sessionStorage.setItem('decodedToken', JSON.stringify(decodedToken));
        sessionStorage.setItem('token', res.token);
        sessionStorage.setItem('idUsuario', decodedToken.sub);
        sessionStorage.setItem('rol', decodedToken.rol);
        this.toastrService.success("Login exitoso", "Información", {closeButton: true});
        this.router.navigate(['/inicio']);
      },
      error => {
        this.error = "Credenciales incorrectas o el usuario no existe";
        this.toastrService.error("Error en el login", "Error", {closeButton: true});
      });
  }
}