import { TestBed } from '@angular/core/testing';

import { GlobalFuctionsService } from './global-fuctions.service';

describe('GlobalFuctionsService', () => {
  let service: GlobalFuctionsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GlobalFuctionsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
