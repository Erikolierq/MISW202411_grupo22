// TrainingPlan model (training-plan.model.ts)
import { Ejercicio } from "../detalles-ejercicio/ejercicio.model";

export interface TrainingPlan {
  id: number;
  name: string;
  description?: string;
  user_id: number;
  exercises: Ejercicio[];
}