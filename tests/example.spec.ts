import { test, expect } from '@playwright/test';

test('test2', async ({ page }) => {
  await page.goto('https://www.amazon.com.mx');
  await expect(page).toHaveTitle(/Amazon.com.mx: Precios bajos /);
  const searchInput = page.locator("input[id='twotabsearchtextbox']");
  await searchInput.fill("Playstation 5");
  await page.click("input[id='nav-search-submit-button']");
  await expect(page.locator("span[class='a-color-state a-text-bold']")).toContainText('Playstation 5')
  await expect(page.locator("h2[class='a-size-medium-plus a-spacing-none a-color-base a-text-bold']")).toContainText('Resultados')
  await expect(page.locator("div[class='s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results_1']")).toBeVisible();
  const product = page.locator("div[class='s-widget-container s-spacing-small s-widget-container-height-small celwidget slot=MAIN template=SEARCH_RESULTS widgetId=search-results_1']");
  await expect(product).toBeVisible();
  await product.first().click();
  await expect(page.locator("span[class='a-size-large product-title-word-break']")).toContainText('Playstation 5');

  
  
  await page.pause();
})