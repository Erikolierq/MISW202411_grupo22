/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { InicioService } from './inicio.service';

describe('Service: Inicio', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [InicioService]
    });
  });

  it('should ...', inject([InicioService], (service: InicioService) => {
    expect(service).toBeTruthy();
  }));
});
