export interface GitHubProfile{
    name:string;
    login:string;
    avatar_url:string;
    bio:string|null;
    location:string|null;
    blog:string|null;
    html_url:string;
    created_at:string;
}

export interface Repository{
    name:string;
    description:string|null;
    stars:number;
    forks:number;
    language:string|null;
    html_url:string;
    updated_at:string;
}

export interface DeveloperAnalytics{
    username:string;
    _from_cache:boolean;
    profile:GitHubProfile;
    metrics:{
        total_repos:number;
        total_stars:number;
        total_forks:number;
        followers:number;
        following:number;
    };
    languages:Record<string,number>;
    top_repositories:Repository[];
}
