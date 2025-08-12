import { Component } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { CommonModule } from '@angular/common';
import { RegisterRequest } from '../../../core/models/user.model';

@Component({
  selector: 'app-register:not(p)',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  templateUrl: './register.html'
})
export class RegisterComponent {
  isLoading = false;
  form;


  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private snack: MatSnackBar,
    private router: Router
  ) {

    this.form = this.fb.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      role: ['User', Validators.required]
    });

  }

  submit() {
    if (this.form.invalid) return;
    this.isLoading = true;

    const payload: RegisterRequest = {
      username: this.form.value.username!,
      email: this.form.value.email!,
      password: this.form.value.password!,
      role: this.form.value.role as 'Organizer' | 'User'
    };
    this.auth.register(payload).subscribe({
      next: () => {
        this.snack.open('Registration successful! Please log in.', 'Close', { duration: 3000 });
        this.router.navigate(['/login']);
        this.isLoading = false;
      },
      error: () => {
        this.snack.open('Registration failed.', 'Close', { duration: 3000 });
        this.isLoading = false;
      }
    });
  }
}
