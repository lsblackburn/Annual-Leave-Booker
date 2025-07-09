import { test, expect } from '@playwright/test';

const baseURL = 'http://127.0.0.1:5000';

// Register a user
async function registerUser(page, { name, email, password }) {
  await page.goto(`${baseURL}/register`);
  await page.getByRole('textbox', { name: 'Enter name' }).fill(name);
  await page.getByRole('textbox', { name: 'Enter email' }).fill(email);
  await page.getByRole('textbox', { name: 'Enter password' }).fill(password);
  await page.getByRole('textbox', { name: 'Enter confirm password' }).fill(password);
  await page.getByRole('button', { name: 'Create an account' }).click();
}

// Log in the user
async function loginUser(page, email, password) {
  await page.goto(`${baseURL}/login`);
  await page.getByRole('textbox', { name: 'Enter email' }).fill(email);
  await page.getByRole('textbox', { name: 'Enter password' }).fill(password);
  await page.getByRole('button', { name: 'Sign in' }).click();
}

test('Without session, redirect to login', async ({ page }) => { // Ensures that without a session, the user is redirected to the login page
  await page.goto(baseURL);
  await page.getByRole('button', { name: 'OK' }).click();
  expect(page.url()).toBe(`${baseURL}/login`);
  await expect(page.getByText('Please log in.')).toBeVisible();
});

test('Registration success', async ({ page }) => { // Tests successful user registration
  const uniqueEmail = `testuser_${Date.now()}@example.com`;
  await registerUser(page, {
    name: 'Test User',
    email: uniqueEmail,
    password: 'Password123!'
  });
  await page.getByRole('button', { name: 'OK' }).click();
  expect(page.url()).toBe(`${baseURL}/login`);
  await expect(page.getByText('Registration successful. Please log in.')).toBeVisible();
});

test('Login fail', async ({ page }) => { // Tests login failure with invalid credentials
  await loginUser(page, 'admin@admin.co.uk', 'Password123!');
  await page.getByRole('button', { name: 'OK' }).click();
  expect(page.url()).toBe(`${baseURL}/login`);
  await expect(page.getByText('Invalid email or password.')).toBeVisible();
});

test.describe('Tests after login', () => { // Tests that require the user to be logged in
  test.beforeEach(async ({ page }) => {
    await loginUser(page, 'admin@admin.com', 'Password123!');
  });

  test('Login success', async ({ page }) => { // Tests successful login
    await page.getByRole('button', { name: 'OK' }).click();
    expect(page.url()).toBe(`${baseURL}/`);
    await expect(page.getByText('Login successful!')).toBeVisible();
  });

  test('Logout success', async ({ page }) => { // Tests successful logout
    await page.getByRole('button', { name: 'OK' }).click();
    await page.getByRole('button', { name: 'Account' }).click();
    await page.getByRole('button', { name: 'Sign out' }).click();
    await page.getByRole('button', { name: 'OK' }).click();
    expect(page.url()).toBe(`${baseURL}/login`);
    await expect(page.getByText('You have been logged out.')).toBeVisible();
  });
});

test.describe('Registration failure tests', () => { // Tests that check various failure scenarios during user registration
  test.beforeEach(async ({ page }) => {
    await page.goto(`${baseURL}/register`);
  });

  test('Secure password enforcement', async ({ page }) => { // Tests that the password meets security requirements
    const uniqueEmail = `testuser_${Date.now()}@example.com`;
    await registerUser(page, {
      name: 'Test User',
      email: uniqueEmail,
      password: 'password' // no uppercase
    });
    await expect(page.getByText('Password must contain at least one uppercase letter.')).toBeVisible();
  });

  test('Email already registered', async ({ page }) => { 
    await registerUser(page, {
      name: 'Name',
      email: 'admin@admin.com',
      password: 'Password123!'
    });
    expect(page.url()).toBe(`${baseURL}/register`);
    await expect(page.getByText('Email is already registered.')).toBeVisible();
  });

  test('Reserved name: Admin', async ({ page }) => { // Tests that the reserved name "Admin" cannot be used for registration
    await registerUser(page, {
      name: 'Admin',
      email: 'admin@admin.com',
      password: 'Password123!'
    });
    expect(page.url()).toBe(`${baseURL}/register`);
    await expect(page.getByText('The name Admin is reserved and cannot be used.')).toBeVisible();
  });
});
