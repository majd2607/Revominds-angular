import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClassifierComponent } from './classifier.component';
import { RouterModule } from '@angular/router';



@NgModule({
  declarations: [
    ClassifierComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild([
      {
        path: '',
        component: ClassifierComponent,
      },
    ]),
  ]
})
export class ClassifierModule { }
