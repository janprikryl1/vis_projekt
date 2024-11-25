export const backendUrl = 'http://127.0.0.1:8000/';

export const toCzechDateFormat = (dateRaw: string): string => {
    const date = new Date(dateRaw);

    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Měsíce jsou 0-indexované
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');

    return `${day}. ${month}. ${year} ${hours}:${minutes}`;
}

export const toCzechRole = (role: string): string => {
    switch (role) {
        case "Teacher":
            return "Učitel";
        case "Pupil":
            return "Žák";
        case "Admin":
            return "Administrator";
        default:
            return "Neznámý role";
    }
}
