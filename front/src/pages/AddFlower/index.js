import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import { withStyles } from '@material-ui/core/styles';
import FormControl from '@material-ui/core/FormControl';
import MenuItem from '@material-ui/core/MenuItem';
import CircularProgress from '@material-ui/core/CircularProgress';
import green from '@material-ui/core/colors/green';
import withRoot from '../../withRoot';

import WebviewControls from 'webview-controls';


const styles = theme => ({
  form: {
    textAlign: 'center',
    padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit}px`,
  },
  input: {
    display: 'none'
  },
  rightIcon: {
    marginLeft: theme.spacing.unit,
  },
  previewImage: {
    maxWidth: '100%',
    maxHeight: '200px',
    height: 'auto',
    margin: 'auto',
    padding: `${theme.spacing.unit}px 0`
  },
  wrapper: {
    margin: theme.spacing.unit,
    position: 'relative',
  },
  buttonSuccess: {
    backgroundColor: green[500],
    '&:hover': {
      backgroundColor: green[700],
    },
  },
  buttonProgress: {
    color: green[500],
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -12,
    marginLeft: -12,
  },
});

const WATERING_PERIODS = [{
  label: 'Raz dziennie',
  value: '1D'
}, {
  label: 'Co 2 dni',
  value: '2D'
}, {
  label: 'Co 3 dni',
  value: '3D'
}, {
  label: 'Co 4 dni',
  value: '4D'
}];

class AddFlower extends React.Component {
  state = {
    name: '',
    image: '',
    imagePreviewUrl: '',
    wateringPeriod: '',
    loading: false,
    success: false,
    error: ''
  };

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  handleSubmit = (e) => {
    this.setState({
      loading: true,
    })
    e.preventDefault();
    const { name, image, wateringPeriod } = this.state;
    const { context } = this.props;
    const form = new FormData();
    form.append('psid', context.psid);
    form.append('name', name);
    form.append('image', image);
    form.append('period', wateringPeriod);

    fetch('/api/flowers/', {
        method: 'post',
        credentials: 'include',
        body: form,
      }
    )
      .then(this.checkStatus)
      .then((data) => {
        this.setState({
          success: true,
          loading: false
        })
        WebviewControls.close();
        console.log('success posting data', data)
      })
      .catch((err) => {
        this.setState({
          loading: false,
          error: err.toString()
        });
        console.error('error posting data', err)
      })
    console.log('handle submit!')
  };


  checkStatus(response) {
    if (response.status >= 200 && response.status < 300) {
      return response;
    }
    const error = new Error(response.statusText);
    error.response = response;
    throw error;
  }


  handleImageChange = (e) => {
    e.preventDefault();
    console.log('image change!');

    let reader = new FileReader();
    let file = e.target.files[0];
    reader.onloadend = () => {
      this.setState({
        image: file,
        imagePreviewUrl: reader.result
      });
    }

    reader.readAsDataURL(file)
  }

  render() {
    const { classes } = this.props;
    const { imagePreviewUrl, name, error, success, loading } = this.state;

    const buttonClassname = classNames({
      [classes.buttonSuccess]: success,
    });

    return (
      <React.Fragment>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="title" color="inherit">
              Dodaj nowy kwiatek
            </Typography>
          </Toolbar>
        </AppBar>
        <form
          className={classes.form}
          noValidate
          autoComplete="off"
          onSubmit={this.handleSubmit}
        >
          <Typography variant="body1" color="inherit">
            Uzupełnij poniższe dane i kliknij przycisk dodaj aby zatwierdzić
          </Typography>
          <TextField
            id="name"
            label="Nazwa kwiatka"
            fullWidth
            value={this.state.name}
            onChange={this.handleChange('name')}
            margin="normal"
          />
          <FormControl
            fullWidth
            margin="normal"
          >
            <input
              id="flower-image"
              type="file"
              accept="image/*"
              className={classes.input}
              onChange={this.handleImageChange}
            />
            <Button
              component="label"
              variant="contained"
              color="secondary"
              htmlFor="flower-image"
            >
              Wybierz zdjęcie kwiatka
              <CloudUploadIcon className={classes.rightIcon} />
            </Button>
            {imagePreviewUrl && (
              <img
                className={classes.previewImage}
                alt="preview"
                src={imagePreviewUrl}
              />
            )}
          </FormControl>
          <TextField
            fullWidth
            id="watering-period"
            select
            label="Czestość podlewania"
            value={this.state.wateringPeriod}
            onChange={this.handleChange('wateringPeriod')}
            helperText="Jak często chcesz podlewać kwiatek?"
            margin="normal"
          >
            {WATERING_PERIODS.map(option => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <div className={classes.wrapper}>
            <Button
              className={buttonClassname}
              type="submit"
              variant="contained"
              color="primary"
              disabled={loading}
            >
              Dodaj {name ? `kwiatek "${name}"` : ''}
            </Button>
            {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
          </div>
          {
            error && (
              <div>
                Error: {error}
              </div>
            )
          }
        </form>
      </React.Fragment>
    );
  }
}

AddFlower.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRoot(withStyles(styles)(AddFlower));
