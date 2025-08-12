import { Component } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBarModule, MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { CommonModule } from '@angular/common';
import { MatIcon } from '@angular/material/icon';
import { LoginRequest } from '../../../core/models/user.model';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSnackBarModule,
    MatIcon
  ],
  templateUrl: './login.html'
})

export class LoginComponent {
  hidePassword = true;
  isLoading = false;
  form;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private snack: MatSnackBar,
    private router: Router
  ) {
    this.form = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', Validators.required]
  });

  }




  submit() {
    if (this.form.invalid) return;

    this.isLoading = true;

    const payload: LoginRequest = {
    email: this.form.value.email!,       // non-null assertion
    password: this.form.value.password!  // non-null assertion
  };

    this.auth.login(payload).subscribe({
      next: () => {
        this.snack.open('Login successful!', 'Close', { duration: 3000 });
        this.router.navigate(['/events']);
        this.isLoading = false;
      },
      error: () => {
        this.snack.open('Login failed. Check credentials.', 'Close', { duration: 3000 });
        this.isLoading = false;
      }
    });
  }
}
