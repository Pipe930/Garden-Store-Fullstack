interface Notifications {
  icon: string;
  subject: string;
  description: string;
}

interface Items {
  icon: string;
  label: string;
}

export const notifications: Array<Notifications> = [

  {
    icon: 'bx bxs-download',
    subject: 'Dowload complete',
    description: 'Lorem ipsum dolor sit amet consectetur.'
  },
  {
    icon: 'bx bxs-cloud-upload',
    subject: 'Upload complete',
    description: 'Lorem ipsum dolor sit amet consectetur adipisicing'
  },
  {
    icon: 'bx bxs-trash',
    subject: '350 MB trash files',
    description: 'Lorem ipsum dolor sit amet consectetur'
  }
]

export const userItems: Array<Items> = [
   {
    icon: 'bx bx-user',
    label: 'Profile'
   },
   {
    icon: 'bx bxs-cog',
    label: 'Settings'
   },
   {
    icon: 'bx bxs-lock-alt',
    label: 'Lock Screen'
   },
   {
    icon: 'bx bxs-log-out',
    label: 'Logout'
   }
]
