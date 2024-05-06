import { Component } from '@angular/core';
import { Service } from '../../service.service';

@Component({
  selector: 'app-recommandation',
  templateUrl: './recommandation.component.html',
  styleUrls: ['./recommandation.component.scss']
})
export class RecommandationComponent {
  userId: number | undefined;
  recommendations: string[] = [];

  constructor(private recommendationService: Service) { }

  getRecommendations() {
    if (!this.userId) {
      console.error("User ID is required.");
      return;
    }
    this.recommendationService.getRecommendations(this.userId)
      .subscribe(
        (response: any) => {
          this.recommendations = response.recommendations;
        },
        (error: any) => {
          console.error("Error occurred while fetching recommendations:", error);
        }
      );
  }
}
