export class TrainingPlan {
    id: number;
    name: string;
    description?: string;
    user_id: number;
    exercises: Exercise[];
  }