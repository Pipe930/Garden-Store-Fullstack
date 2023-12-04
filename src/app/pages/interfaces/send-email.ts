export interface SendEmail {
  full_name: string;
  email: string;
  message: string;
}

export interface SendEmailResponse{
  status: string;
  data: SendEmail;
  message: string;
}
