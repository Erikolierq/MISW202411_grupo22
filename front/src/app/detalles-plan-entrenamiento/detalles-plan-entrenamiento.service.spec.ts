/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { DetallesPlanEntrenamientoService } from './detalles-plan-entrenamiento.service';

describe('Service: DetallesPlanEntrenamiento', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DetallesPlanEntrenamientoService]
    });
  });

  it('should ...', inject([DetallesPlanEntrenamientoService], (service: DetallesPlanEntrenamientoService) => {
    expect(service).toBeTruthy();
  }));
});
