import React from "react";
import { reatomComponent } from "@reatom/npm-react";
import { Container, Anchor, Group, Burger, Box } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";

import { countries, countryAtom, updateCountry, type Countries } from "../model";
import classes from './CountriesList.module.css';

const CountriesList = reatomComponent(({ ctx }) => {
  const [opened, { toggle }] = useDisclosure(false);

  const changeCountry = (e: React.MouseEvent<HTMLButtonElement>) => {
    const country = e.currentTarget.dataset.country;
    if (country) {
      updateCountry(ctx, country as Countries);
    }
  };

  const mainItems = countries.map((item) => (
    <Anchor<"a">
      href={item.path}
      key={item.name}
      // className={classes.mainLink}
      data-active={ctx.get(countryAtom) === item.name}
      onClick={changeCountry}
    >
      {item.label}
    </Anchor>
  ));

  return (
    <header className={classes.header}>
      <Container className={classes.inner}>
        <Box className={classes.links} visibleFrom="sm">
          <Group gap={0} justify="flex-end" className={classes.mainLinks}>
            {mainItems}
          </Group>
        </Box>
        <Burger
          opened={opened}
          onClick={toggle}
          className={classes.burger}
          size="sm"
          hiddenFrom="sm"
        />
      </Container>
    </header>
  );
}, "CountriesList");

export default CountriesList;
