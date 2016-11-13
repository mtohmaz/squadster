import { Component } from '@angular/core';
import { Router } from "@angular/router";

@Component({
  selector: 'login',
  templateUrl: 'html/login.component.html'
})

export class LoginComponent {
  loggedIn: boolean = false;

  constructor(
      private router: Router
  ){}

  login() {
    this.loggedIn = !this.loggedIn;
    this.router.navigate(['app/list-view']);
  }
}
