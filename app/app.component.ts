import {Component} from '@angular/core';
//import {CreateComponent} from './create.component';

@Component({
    selector: 'my-app',
    template: `
    <h1>Hello Angular</h1>
    <create></create>
    `,
    //state which components are used in the template.
    //directives: [CreateComponent]
})
export class AppComponent { }
