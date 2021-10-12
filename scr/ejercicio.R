library(tidyverse)
library(FactoMineR)

dat = read_csv("Downloads/ejercicio_juana.csv")

dat2 <- dat[,c(
    "opinion_gestion_alberto",
    "opinion_gestion_kicillof",
    "opinion_tolosapaz",
    "opinion_manes",
    "opinion_santilli",
    "posibilidad_voto_tolosapaz",
    "posibilidad_voto_santilli",
    "posibilidad_voto_manes"
)]

fit <- PCA(dat2)

latente <- as_tibble(fit$ind$coord[,1:2])
latente$intencion_voto_2021 <- dat$intencion_voto_2021
colnames(latente)[1:2] <- c("Dim.1","Dim.2")

centroides <- latente %>%
    group_by(intencion_voto_2021) %>%
    summarise(
        Dim.1 = mean(Dim.1),
        Dim.2 = mean(Dim.2)
        ) %>%
    filter(!intencion_voto_2021%in%"0")

plott <- ggplot() +
    geom_point(
        data=latente,
        aes(x=Dim.1,y=Dim.2),size=.4,col="darkgrey"
    ) +
    geom_segment(
        data=centroides,
        aes(
            x = 0, y = 0,
            xend = Dim.1, yend = Dim.2,
            group=intencion_voto_2021,
            col=intencion_voto_2021,
            ),
        size=1.5,
        arrow = arrow(length = unit(0.35, "cm"))
        )+
    geom_line() +
    theme_minimal() +
    xlab("Dim1: Juntos vs. Frente (63.06%)") +
    ylab("Dim2: Segundas Fuerzas (14.09%)")

plott
