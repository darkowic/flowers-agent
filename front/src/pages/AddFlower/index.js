import React from 'react';
import PropTypes from 'prop-types';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import { withStyles } from '@material-ui/core/styles';
import FormControl from '@material-ui/core/FormControl';
import MenuItem from '@material-ui/core/MenuItem';
import withRoot from '../../withRoot';


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
  }
});

const WATERING_PERIODS = [{
  label: 'Raz dziennie',
  value: '1d'
}, {
  label: 'Co 2 dni',
  value: '2d'
}, {
  label: 'Co 3 dni',
  value: '3d'
}, {
  label: 'Co 4 dni',
  value: '4d'
}];

class AddFlower extends React.Component {
  state = {
    name: '',
    image: '',
    imagePreviewUrl: '',
    wateringPeriod: ''
  };

  handleClose = () => {
    this.setState({
      open: false,
    });
  };

  handleClick = () => {
    this.setState({
      open: true,
    });
  };

  handleChange = name => event => {
    this.setState({
      [name]: event.target.value,
    });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    console.log('handle submit!')
  };

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
    const { imagePreviewUrl, name } = this.state;

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
          <Button
            type="submit"
            variant="contained"
            color="primary"
          >
            Dodaj {name ? `kwiatek "${name}"` : ''}
          </Button>
        </form>
      </React.Fragment>
    );
  }
}

AddFlower.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withRoot(withStyles(styles)(AddFlower));
