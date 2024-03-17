export interface Ejercicio {
    id: number;
    name: string;
    description?: string; // La descripción es opcional
    type?: string; // El tipo es opcional
    duration?: number;
    repetitions?: number;
  }