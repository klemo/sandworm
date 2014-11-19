'use strict';

describe('Sandowrm App', function() {

    it('should redirect to login', function() {
        browser.driver.get('http://localhost:8080/#/');
        expect(browser.getCurrentUrl()).toEqual('http://localhost:8080/#/login');
    });

    it('should display login form', function() {
        browser.driver.get('http://localhost:8080/#/');
        expect(element(by.css('.signin-link')).isDisplayed())
            .toBe(true);
    });

    describe('Basic lab list', function() {

        it('should login user', function() {
            browser.get('http://localhost:8080/#/');
            var username = element(
                by.model('ctrl.user.username'));
            var password = element(
                by.model('ctrl.user.password'));
            username.sendKeys('test');
            password.sendKeys('test');
            element(by.css('.btn.btn-primary')).click();
            expect(element(by.css('.signout-link')).isDisplayed())
                .toBe(true);
        });

        it('should display basic labs page', function() {
            var labList = element.all(by.repeater('lab in labCtrl.labs'));
            expect(labList.count()).toBe(2);
        });

        describe('Lab details', function() {
            
            beforeEach(function() {
                browser.driver.get('http://localhost:8080/#/labs/lab-1');
            });

            it('should display lab details page', function() {    
                expect(element(by.binding('ctrl.lab.name')).getText()).toBe('LAB1');
            });
        });

        it('should sign out current user', function() {
            browser.driver.get('http://localhost:8080/#/');
            element(by.css('.signout-link')).click();
            expect(browser.getCurrentUrl()).toEqual('http://localhost:8080/#/login');
            expect(element(by.css('.signin-link')).isDisplayed())
                .toBe(true);
        });

        it('should redirect to login when accessing private resource', function() {
            browser.driver.get('http://localhost:8080/#/labs/lab-1');
            expect(browser.getCurrentUrl()).toEqual('http://localhost:8080/#/login');
        });
    });
});