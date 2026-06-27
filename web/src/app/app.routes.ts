import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: '',
        loadChildren: () =>
            import('./modules/home/home.routes')
                .then(m => m.HOME_ROUTES)
    },
    {
        path: 'app',
        loadChildren: () =>
            import('./modules/game/game.routes')
                .then(m => m.GAME_ROUTES)
    },
    {
        path: 'profile',
        loadChildren: () =>
            import('./modules/profile/profile.routes')
                .then(m => m.PROFILE_ROUTES)
    }
];
