import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecommandationComponent } from './recommandation.component';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';



@NgModule({
  declarations: [
    RecommandationComponent
  ],
  imports: [
    CommonModule,  
     RouterModule.forChild([
      {
        path: '',
        component: RecommandationComponent,
      },
    ]),
    FormsModule
  ]
})
export class RecommandationModule { }
