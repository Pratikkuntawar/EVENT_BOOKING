import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageEvent } from './manage-event';

describe('ManageEvent', () => {
  let component: ManageEvent;
  let fixture: ComponentFixture<ManageEvent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ManageEvent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ManageEvent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
