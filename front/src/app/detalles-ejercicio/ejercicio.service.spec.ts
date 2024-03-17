/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { EjercicioService } from './ejercicio.service';

describe('Service: Ejercicio', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [EjercicioService]
    });
  });

  it('should ...', inject([EjercicioService], (service: EjercicioService) => {
    expect(service).toBeTruthy();
  }));
});
