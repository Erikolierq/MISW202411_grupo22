export class Usuario {
    constructor(
        public id: number,
        public usuario: string,
        public contrasena: string,
        public rol: string,
        public correo: string,
        public nombre?: string,
        public numeroContacto?: string,
    ) {}
}