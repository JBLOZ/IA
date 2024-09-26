printf "Indica los procesos que quieras ver: "
read N


ps -aux --sort=-%mem | head -n $(($N+1))
